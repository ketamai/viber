/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'wow-gold': '#f8b700',
        'wow-brown': '#2d2018',
        'wow-dark': '#211510',
        'wow-light': '#f8f3e3',
        'horde': '#b30000',
        'alliance': '#0078ff',
        'neutral': '#85754d',
      },
      fontFamily: {
        'wow': ['LifeCraft', 'Palatino Linotype', 'Book Antiqua', 'Palatino', 'serif'],
        'body': ['Roboto', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'wow': '0 4px 6px -1px rgba(0, 0, 0, 0.6), 0 2px 4px -1px rgba(0, 0, 0, 0.4)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
} 