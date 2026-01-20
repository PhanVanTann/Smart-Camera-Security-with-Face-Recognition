# Smart Security Camera Dashboard

Modern web-based dashboard UI for smart security camera system with face recognition and mask detection.

## Features

- 📊 **Overview Dashboard** - Real-time statistics and system status
- 📹 **Camera Monitor** - Live feed with AI detection overlays
- 👥 **Residents Management** - Add and manage registered residents
- ⚠️ **Strangers & Alerts** - Track unknown visitors
- 😷 **Mask Analysis** - Monitor mask compliance
- 📜 **History Logs** - Complete detection history
- ⚙️ **Settings** - Configure system parameters

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development
- **React Router** for navigation
- **Recharts** for data visualization
- **Pure CSS** with dark mode design system

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Design Features

- Dark mode first design
- Smooth animations and transitions
- Responsive layout (desktop & tablet)
- Modern glassmorphism effects
- Professional security-oriented UI

## Project Structure

```
UI/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── index.css       # Design system & global styles
│   ├── App.tsx         # Main app with routing
│   └── main.tsx        # Entry point
├── index.html
├── package.json
└── vite.config.ts
```

## License

MIT
