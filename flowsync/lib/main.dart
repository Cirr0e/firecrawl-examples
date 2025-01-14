import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'screens/home_screen.dart';
import 'screens/workspace_screen.dart';
import 'screens/ai_assistant_screen.dart';
import 'services/theme_service.dart';

void main() {
  runApp(
    ProviderScope(
      child: FlowSyncApp(),
    ),
  );
}

class FlowSyncApp extends ConsumerWidget {
  final _router = GoRouter(
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/workspace/:id',
        builder: (context, state) => WorkspaceScreen(
          workspaceId: state.params['id']!,
        ),
      ),
      GoRoute(
        path: '/ai-assistant',
        builder: (context, state) => const AIAssistantScreen(),
      ),
    ],
  );

  FlowSyncApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);

    return MaterialApp.router(
      title: 'FlowSync',
      theme: ref.read(themeServiceProvider).lightTheme,
      darkTheme: ref.read(themeServiceProvider).darkTheme,
      themeMode: themeMode,
      routerConfig: _router,
    );
  }
}