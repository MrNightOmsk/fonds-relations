/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0891b2',
          dark: '#3ABBB3',
          light: '#22d3ee',
        },
        secondary: {
          DEFAULT: '#10b981',
          dark: '#06b6d4',
          light: '#34d399',
        },
        danger: {
          DEFAULT: '#ef4444',
          dark: '#dc2626',
          light: '#f87171',
        },
        success: {
          DEFAULT: '#10b981',
          dark: '#059669',
          light: '#34d399',
        },
        warning: {
          DEFAULT: '#f59e0b',
          dark: '#d97706',
          light: '#fbbf24',
        },
        background: {
          light: '#ffffff',
          dark: '#1e1e2e',
        },
        surface: {
          light: '#f3f4f6',
          dark: '#252536',
        },
        text: {
          light: '#111827',
          dark: '#f8f9fa',
          secondary: {
            light: '#4b5563',
            dark: '#9ca3af',
          }
        },
        border: {
          light: '#d1d5db',
          dark: '#374151',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card-dark': '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.18)',
      },
      transitionProperty: {
        height: 'height',
        width: 'width',
        spacing: 'margin, padding',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        light: {
          "primary": "#0891b2",
          "secondary": "#10b981",
          "accent": "#0ea5e9",
          "neutral": "#111827",
          "base-100": "#ffffff",
          "base-200": "#f3f4f6",
          "base-300": "#e5e7eb",
          "info": "#3abff8",
          "success": "#10b981",
          "warning": "#f59e0b",
          "error": "#ef4444",
        },
        dark: {
          "primary": "#3ABBB3",
          "secondary": "#06b6d4",
          "accent": "#0ea5e9",
          "neutral": "#f8f9fa",
          "base-100": "#1e1e2e",
          "base-200": "#252536",
          "base-300": "#2a2a3c",
          "info": "#3abff8",
          "success": "#10b981",
          "warning": "#f59e0b",
          "error": "#ef4444",
        },
      },
    ],
  },
}; 