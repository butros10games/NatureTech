/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html', './static/**/*.js'],
  theme: {
    extend: {
      colors: {
        'green-main': '#355E3B',
        'green-hover': '#496e4f',
      },
      height: {
        'mobile-full': 'calc((var(--vh, 1vh) * 100) - 64px)',
      },
    },
  },
  plugins: [],
}
