module.exports = {
  content: [
    "./templates/**/*.html",   // Folder templates untuk HTML Flask
    "./static/src/**/*.js",    // Folder untuk file JS
    "./node_modules/flowbite/**/*.js" // Tambahkan path ke Flowbite
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("flowbite/plugin") // Tambahkan plugin Flowbite
  ],
}