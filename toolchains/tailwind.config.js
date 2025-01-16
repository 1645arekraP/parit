/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./pg_app/templates/pg_app/**/*.html'],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require('daisyui'),
  ],
}

