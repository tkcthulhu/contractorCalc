import 'package:contractorcalc/app.dart';
import 'package:contractorcalc/main.dart' as entrypoint;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('real entrypoint shows an honest, noninteractive foundation', (
    tester,
  ) async {
    entrypoint.main();
    await tester.pumpAndSettle();

    expect(find.byType(ProviderScope), findsOneWidget);
    expect(find.byType(ContractorCalcApp), findsOneWidget);
    expect(find.text('ContractorCalc'), findsOneWidget);
    expect(find.text('Project foundation'), findsOneWidget);
    expect(
      find.textContaining('Calculations and saved data are not available yet.'),
      findsOneWidget,
    );
    expect(find.byType(FloatingActionButton), findsNothing);
    expect(find.byType(EditableText), findsNothing);
    expect(tester.takeException(), isNull);
  });

  testWidgets('foundation remains readable on a small screen with large text', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(320, 568);
    tester.view.devicePixelRatio = 1;
    tester.platformDispatcher.textScaleFactorTestValue = 2;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);
    final semantics = tester.ensureSemantics();
    try {
      entrypoint.main();
      await tester.pumpAndSettle();
      await tester.ensureVisible(
        find.textContaining('unfinished development build'),
      );

      expect(find.bySemanticsLabel('Project foundation'), findsOneWidget);
      expect(tester.takeException(), isNull);
    } finally {
      semantics.dispose();
    }
  });
}
