/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                herba: {
                    50: '#f4f9f4',  // Very light mint for background
                    100: '#e3f0e3',
                    200: '#c5e0c5',
                    300: '#9bc89b',
                    400: '#6fae6f',
                    500: '#4c934c', // Primary sage
                    600: '#3a753a',
                    700: '#2f5d2f',
                    800: '#284a28',
                    900: '#213d21',
                },
                teal: {
                    50: '#f0f9fa',
                    100: '#d9f0f2',
                    500: '#14b8a6', // Standard teal
                    600: '#0d9488',
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
