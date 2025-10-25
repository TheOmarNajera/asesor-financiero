import React from 'react';

const BanorteLogo = ({ className = "h-8 w-8", showText = true }) => {
  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      {/* Logo SVG de Banorte */}
      <div className="flex-shrink-0">
        <svg 
          width="32" 
          height="32" 
          viewBox="0 0 32 32" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
          className="h-8 w-8"
        >
          {/* Círculo rojo de Banorte */}
          <circle cx="16" cy="16" r="16" fill="#EB0029"/>
          
          {/* Letra "B" estilizada */}
          <path 
            d="M10 8h8c2.2 0 4 1.8 4 4s-1.8 4-4 4h-2v4h-2V8zm2 2v4h6c1.1 0 2-.9 2-2s-.9-2-2-2h-6z" 
            fill="white"
          />
          
          {/* Elementos decorativos */}
          <circle cx="22" cy="10" r="1.5" fill="white" opacity="0.8"/>
          <circle cx="24" cy="14" r="1" fill="white" opacity="0.6"/>
        </svg>
      </div>
      
      {/* Texto del logo */}
      {showText && (
        <div className="flex flex-col">
          <span className="text-lg font-bold text-banorte-primary font-display">
            Banorte
          </span>
          <span className="text-xs text-banorte-accent font-medium">
            Asesor PyME
          </span>
        </div>
      )}
    </div>
  );
};

export default BanorteLogo;
