# Development Guide

## React DevTools Setup

This project includes React DevTools for enhanced development experience.

### Option 1: Browser Extension (Recommended)
1. Install React DevTools browser extension:
   - [Chrome Extension](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
   - [Firefox Extension](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/)

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000`
4. Open Developer Tools (F12) and you'll see a "React" tab

### Option 2: Standalone DevTools
1. Run the development server with React DevTools:
   ```bash
   npm run dev:tools
   ```

2. This will open React DevTools in a separate window
3. Your app will be available at `http://localhost:3000`

### Option 3: Built-in DevTools
The app automatically loads React DevTools in development mode when you run:
```bash
npm run dev
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run dev:tools` - Start development server with React DevTools
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Development Features

### 🔧 React DevTools Features:
- **Component Tree**: Inspect component hierarchy
- **Props & State**: View and modify component props and state
- **Profiler**: Performance analysis and optimization
- **Hooks**: Debug React hooks and their values
- **Context**: Inspect React Context providers and consumers

### 🎨 Development Tools:
- **Hot Reload**: Automatic page refresh on code changes
- **TypeScript**: Full type checking and IntelliSense
- **ESLint**: Code quality and style enforcement
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and development server

## Debugging Tips

1. **Component Inspection**: Use React DevTools to inspect component props and state
2. **Performance**: Use the Profiler tab to identify performance bottlenecks
3. **State Management**: Monitor CartProvider state changes in real-time
4. **Network**: Use browser DevTools to monitor API calls
5. **Console**: Check for warnings and errors in the browser console

## Environment Variables

- `NODE_ENV=development` - Enables React DevTools and development features
- `VITE_API_URL` - Backend API URL (if needed)

## Troubleshooting

### React DevTools not showing:
1. Make sure you're in development mode (`NODE_ENV=development`)
2. Check browser console for any errors
3. Try refreshing the page
4. Install the browser extension as a fallback

### Performance Issues:
1. Use React DevTools Profiler to identify slow components
2. Check for unnecessary re-renders
3. Optimize with React.memo and useMemo where appropriate 