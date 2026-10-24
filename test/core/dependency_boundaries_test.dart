import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

const _pureDartLibraries = {
  'dart:async',
  'dart:collection',
  'dart:convert',
  'dart:core',
  'dart:math',
  'dart:typed_data',
};

bool _isAllowedCoreDependency(Uri source, String dependency) {
  if (dependency.startsWith('dart:')) {
    return _pureDartLibraries.contains(dependency);
  }
  if (dependency.startsWith('package:')) {
    return Uri.parse(dependency)
        .normalizePath()
        .path
        .startsWith('contractorcalc/core/');
  }
  final target = source.resolve(dependency).normalizePath();
  return target.scheme == 'file' &&
      target.path.startsWith(Directory('lib/core').absolute.uri.path);
}

Iterable<String> _dependencies(String source) sync* {
  final directives = RegExp(
    r'\b(?:import|export|part)\s+([^;]+);',
    dotAll: true,
  );
  final uris = RegExp('''['"]([^'"]+)['"]''');
  for (final directive in directives.allMatches(source)) {
    for (final uri in uris.allMatches(directive.group(1)!)) {
      yield uri.group(1)!;
    }
  }
}

void main() {
  test('core guard rejects frameworks, platform APIs, and outward paths', () {
    final source = Directory('lib/core').absolute.uri.resolve('quantity.dart');
    for (final dependency in [
      'dart:math',
      'package:contractorcalc/core/units.dart',
      'units.dart',
    ]) {
      expect(_isAllowedCoreDependency(source, dependency), isTrue);
    }
    for (final dependency in [
      'dart:io',
      'dart:ffi',
      'dart:ui',
      'package:flutter/widgets.dart',
      'package:flutter_riverpod/flutter_riverpod.dart',
      'package:drift/drift.dart',
      'package:contractorcalc/data/database.dart',
      'package:contractorcalc/core/../data/database.dart',
      '../data/database.dart',
      'https://example.com/remote.dart',
    ]) {
      expect(
        _isAllowedCoreDependency(source, dependency),
        isFalse,
        reason: dependency,
      );
    }
  });

  test('guard inspects export, part and every conditional import target', () {
    expect(
      _dependencies('''
import 'safe.dart' if (dart.library.io) 'dart:io';
export 'api.dart';
part 'quantity.g.dart';
'''),
      ['safe.dart', 'dart:io', 'api.dart', 'quantity.g.dart'],
    );
  });

  test(
    'production core has no framework, storage, or platform dependencies',
    () {
      final core = Directory('lib/core');
      expect(core.existsSync(), isTrue);
      for (final file in core.listSync(recursive: true).whereType<File>()) {
        if (!file.path.endsWith('.dart')) continue;
        for (final dependency in _dependencies(file.readAsStringSync())) {
          expect(
            _isAllowedCoreDependency(file.absolute.uri, dependency),
            isTrue,
            reason: '${file.path} must not depend on $dependency',
          );
        }
      }
    },
  );
}
