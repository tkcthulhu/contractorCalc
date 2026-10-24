import 'package:flutter/material.dart';

import 'features/foundation/foundation_screen.dart';

class ContractorCalcApp extends StatelessWidget {
  const ContractorCalcApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ContractorCalc',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorSchemeSeed: const Color(0xFF315B45)),
      home: const FoundationScreen(),
    );
  }
}
