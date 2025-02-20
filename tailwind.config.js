/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pg_app/templates/pg_app/**/*.html',
    "./static/src/**/*.{html,js,css}"
  ],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: ["emerald", "dim"],
  },
  plugins: [
    require("@tailwindcss/typography"),
    require('daisyui'),
  ],
}

