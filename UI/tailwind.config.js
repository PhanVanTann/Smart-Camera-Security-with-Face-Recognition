/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark mode colors
        'bg-primary': '#0a0e1a',
        'bg-secondary': '#111827',
        'bg-tertiary': '#1a2332',
        'bg-card': '#1e293b',
        'bg-hover': '#2d3a52',
        
        // Accent colors
        'accent-primary': '#3b82f6',
        'accent-secondary': '#8b5cf6',
        'accent-success': '#10b981',
        'accent-warning': '#f59e0b',
        'accent-danger': '#ef4444',
        'accent-info': '#06b6d4',
        
        // Text colors
        'text-primary': '#f8fafc',
        'text-secondary': '#cbd5e1',
        'text-tertiary': '#94a3b8',
        'text-disabled': '#64748b',
        
        // Border colors
        'border-primary': '#334155',
        'border-secondary': '#475569',
        'border-hover': '#64748b',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      boxShadow: {
        'glow': '0 0 20px rgba(59, 130, 246, 0.3)',
        'glow-success': '0 0 20px rgba(16, 185, 129, 0.3)',
        'glow-danger': '0 0 20px rgba(239, 68, 68, 0.3)',
      },
      animation: {
        'pulse-slow': 'pulse 2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
