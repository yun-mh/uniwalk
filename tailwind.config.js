module.exports = {
  theme: {
    extend: {
      inset: {
        "0": 0,
        "1/2": "50%",
        "-half": "-50%"
      },
      spacing: {
        "18": "4.5rem",
        "26": "6.5rem",
        "28": "7rem",
        "36": "9rem",
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",
        "75vw": "75%",
        "80vw": "80%",
        "90vw": "90%"
      },
      height: {
        "1/2": "50%",
        "1/3": "33.3%",
        "2/3": "66.6%"
      },
      minWidth: {
        "0": "0",
        "1/5": "20%",
        "1/2": "50%",
        full: "100%"
      },
      minHeight: {
        "0": "0",
        "1/4": "25%",
        "1/2": "50%",
        "3/4": "75%",
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh"
      },
      borderRadius: {
        xl: "1.5rem"
      },
      colors: {
        universe: {
          lighter: "#2B3D4E",
          dark: "#1C2934"
        },
        home: {
          gray: "#322f38",
          blue: "#366ccf"
        }
      }
    },
    boxShadow: {
      dark:
        " 0 4px 6px -1px rgba(0, 0, 0, .2), 0 2px 4px -1px rgba(0, 0, 0, .08)",
      default: "0 1px 3px 0 rgba(0, 0, 0, .1), 0 1px 2px 0 rgba(0, 0, 0, .06)",
      md:
        " 0 4px 6px -1px rgba(0, 0, 0, .1), 0 2px 4px -1px rgba(0, 0, 0, .06)",
      lg:
        " 0 10px 15px -3px rgba(0, 0, 0, .1), 0 4px 6px -2px rgba(0, 0, 0, .05)"
    }
  },
  variants: {},
  plugins: []
};
