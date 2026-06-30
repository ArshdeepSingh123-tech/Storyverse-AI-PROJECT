/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#f5f0ff',
          100: '#ede0ff',
          200: '#d9bfff',
          300: '#bf94ff',
          400: '#a066ff',
          500: '#8542f5',
          600: '#6C3FC5',
          700: '#5a33a3',
          800: '#472880',
          900: '#2d1a52',
          950: '#1a0d33',
        },
        ink: {
          50:  '#f8f8fc',
          100: '#f0f0f8',
          200: '#e0e0f0',
          300: '#c0c0d8',
          400: '#9090b8',
          500: '#606090',
          600: '#404070',
          700: '#282855',
          800: '#181840',
          900: '#0c0c28',
          950: '#06060f',
        },
      },
      fontFamily: {
        display: ['var(--font-display)', 'Georgia', 'serif'],
        body: ['var(--font-body)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'monospace'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'brand-gradient': 'linear-gradient(135deg, #6C3FC5 0%, #a066ff 50%, #bf94ff 100%)',
        'dark-mesh': 'radial-gradient(ellipse at 20% 50%, rgba(108,63,197,0.15) 0%, transparent 60%), radial-gradient(ellipse at 80% 20%, rgba(160,102,255,0.1) 0%, transparent 60%)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'shimmer': 'shimmer 2s linear infinite',
        'fade-up': 'fadeUp 0.5s ease-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-12px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(108,63,197,0.3)' },
          '100%': { boxShadow: '0 0 40px rgba(160,102,255,0.6)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(-16px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
