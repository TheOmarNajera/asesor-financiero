// Configuración de Tailwind CSS con paleta de colores de Banorte
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta de colores de Banorte actualizada
        banorte: {
          primary: '#EB0029',      // Rojo principal de Banorte
          secondary: '#49474',     // Gris fondo
          accent: '#7B868C',      // Gris iconos
          success: '#00AA44',     // Verde para éxito
          warning: '#FF9900',     // Amarillo para advertencias
          danger: '#EB0029',      // Rojo para errores (mismo que primary)
          light: '#F5F8FA',      // Gris claro
          dark: '#49474',        // Gris oscuro
          white: '#FFFFFF',      // Blanco puro
        },
        // Colores adicionales para el sistema financiero
        financial: {
          income: '#00AA44',     // Verde para ingresos
          expense: '#EB0029',     // Rojo para gastos
          profit: '#0066CC',      // Azul para ganancias
          neutral: '#7B868C',     // Gris neutro
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        'banorte': '0 4px 20px rgba(235, 0, 41, 0.1)',
        'banorte-lg': '0 8px 30px rgba(235, 0, 41, 0.15)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 3s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
