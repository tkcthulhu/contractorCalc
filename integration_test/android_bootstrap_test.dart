import 'dart:convert';
import 'dart:io';

import 'package:contractorcalc/main.dart' as entrypoint;
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:sqlite3/sqlite3.dart';

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Android foundation and bundled SQLite bootstrap', (
    tester,
  ) async {
    expect(Platform.isAndroid, isTrue);
    entrypoint.main();
    await tester.pumpAndSettle();
    expect(find.text('ContractorCalc'), findsOneWidget);
    expect(find.text('Project foundation'), findsOneWidget);
    expect(find.textContaining('unfinished development build'), findsOneWidget);
    expect(tester.takeException(), isNull);

    final database = sqlite3.openInMemory();
    try {
      final identity = database
          .select(
            'SELECT sqlite_version() AS version, sqlite_source_id() AS source_id',
          )
          .single;
      final options = database.select('PRAGMA compile_options');
      expect(database.select('SELECT 1 + 1 AS answer').single['answer'], 2);
      expect(identity['version'], isA<String>());
      expect(identity['source_id'], isA<String>());
      expect(options, isNotEmpty);
      final report = <String, dynamic>{
        'sqlite_version': identity['version'],
        'sqlite_source_id': identity['source_id'],
        'sqlite_compile_options': [
          for (final row in options) row.values.single,
        ],
      };
      binding.reportData = report;
      debugPrint('ANDROID_BOOTSTRAP_SQLITE=${jsonEncode(report)}');
    } finally {
      database.close();
    }
  });
}
