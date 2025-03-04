/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3498db',
          dark: '#2980b9',
          light: '#5faee3',
        },
        secondary: {
          DEFAULT: '#2ecc71',
          dark: '#27ae60',
          light: '#5fd48e',
        },
        danger: {
          DEFAULT: '#e74c3c',
          dark: '#c0392b',
          light: '#ed7669',
        },
        background: '#f5f5f5',
        text: '#2c3e50',
      },
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
          "primary": "#3498db",
          "secondary": "#2ecc71",
          "accent": "#e67e22",
          "neutral": "#2c3e50",
          "base-100": "#f5f5f5",
          "info": "#3abff8",
          "success": "#36d399",
          "warning": "#f59f0b",
          "error": "#e74c3c",
        },
        dark: {
          "primary": "#5faee3",
          "secondary": "#5fd48e",
          "accent": "#f39c12",
          "neutral": "#ecf0f1",
          "base-100": "#2c3e50",
          "info": "#3abff8",
          "success": "#36d399",
          "warning": "#fbbd23",
          "error": "#ed7669",
        },
      },
    ],
  },
}; 