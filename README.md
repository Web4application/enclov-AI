<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <h1> Enclov AI </h1>

  <!-- Load Enclov AI script asynchronously -->
  <script
    src="https://enclov-dkbdfezwi-web4application.vercel.app"
    async
    onload="initEnclovApp()"
    onerror="showError('⚠️ Failed to load Enclov AI script')">

  </body
  {
      font-family: "Inter", Arial, sans-serif;
      background-color: #050505;
      color: #e8e8e8;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      overflow: hidden;
    }

    h1 {
      color: #00ffc6;
      font-size: 2rem;
      margin-bottom: 0.5rem;
      text-shadow: 0 0 20px #00ffc6;
    }

    p {
      font-size: 1rem;
      color: #aaa;
      margin-top: 0;
      margin-bottom: 2rem;
    }

    /* Loader reactor animation */
    .loader {
      width: 90px;
      height: 90px;
      border-radius: 50%;
      background: radial-gradient(circle at center, #00ffc6, transparent 70%);
      box-shadow: 0 0 40px #00ffc6;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      animation: reactor-spin 2s linear infinite, glow 2s ease-in-out infinite alternate;
      transition: all 1s ease-in-out;
    }

    @keyframes reactor-spin {
      0% { transform: rotate(0deg) scale(1); }
      100% { transform: rotate(360deg) scale(1.1); }
    }

    @keyframes glow {
      0% { box-shadow: 0 0 15px #00ffc6; opacity: 0.7; }
      100% { box-shadow: 0 0 50px #00ffc6; opacity: 1; }
    }

    @keyframes revealLogo {
      0% { transform: scale(0.4) rotate(-90deg); opacity: 0; filter: blur(5px); }
      100% { transform: scale(1) rotate(0deg); opacity: 1; filter: blur(0); }
    }

    .status {
      margin-top: 1.5rem;
      font-size: 1rem;
      color: #b0b0b0;
    }

    .success {
      color: #00ffc6;
      text-shadow: 0 0 10px #00ffc6;
    }

    .error {
      color: #ff4444;
      text-shadow: 0 0 10px #ff4444;
    }

    /* Enclov logo reveal with spin + glow */
    .enclov-logo {
      width: 70px;
      height: 70px;
      background-image: url('https://raw.githubusercontent.com/Web4application/enclov-AI/main/assets/enclov-logo.png');
      background-size: contain;
      background-repeat: no-repeat;
      opacity: 0;
      animation: revealLogo 1.2s ease-out forwards, logo-pulse 3s ease-in-out infinite alternate;
      filter: drop-shadow(0 0 20px #00ffc6);
    }

    @keyframes logo-pulse {
      0% { filter: drop-shadow(0 0 10px #00ffc6); transform: scale(1); }
      100% { filter: drop-shadow(0 0 25px #00ffc6); transform: scale(1.05); }
    }

    /* Badge */
    a img {
      margin-top: 3rem;
      border: none;
      height: 22px;
    }

    @keyframes shake {
      0% { transform: translateX(-3px); }
      100% { transform: translateX(3px); }
    } </style><script/></head><body>
 <p/>
  </h2>Welcome to Enclov AI</h2>
  
  <h3>Powered by Web4Application</h3>
  <p>
  <div id="loader" class="loader"></div>
  <div id="status" class="status">⏳ Initializing Enclov AI...</div>

  <!-- GitHub Actions build badge -->
  <a href="https://github.com/Web4application/enclov-AI/actions/workflows/deploy-docs.yml" target="_blank">
    <img 
      src="https://github.com/Web4application/enclov-AI/actions/workflows/deploy-docs.yml/badge.svg" 
      alt="Build and Deploy Enclov CLI Docs" 
    />
  </a>

  <noscript>
    <p style="color: red;">⚠️ JavaScript is disabled. Enclov AI features won’t work properly.</p>
  </noscript>

  <script>
    function initEnclovApp() {
      const loader = document.getElementById('loader');
      const statusEl = document.getElementById('status');

      // Simulate boot sequence timing
      setTimeout(() => {
        try {
          if (typeof Enclov !== 'undefined' && typeof Enclov.start === 'function') {
            Enclov.start();
            console.log('🚀 Enclov AI started successfully.');
          }

          // Power-on transition
          loader.style.animation = 'none';
          loader.style.background = 'transparent';
          loader.style.boxShadow = 'none';
          loader.innerHTML = '<div class="enclov-logo"></div>';

          statusEl.textContent = '✅ Enclov AI is online.';
          statusEl.classList.add('success');
        } catch (err) {
          showError('💥 Error during Enclov initialization');
          console.error(err);
        }
      }, 2000);
    }

    function showError(message) {
      const loader = document.getElementById('loader');
      const statusEl = document.getElementById('status');
      loader.style.background = 'radial-gradient(circle, #ff4444, transparent 70%)';
      loader.style.animation = 'shake 0.4s infinite alternate';
      loader.style.boxShadow = '0 0 20px #ff4444';
      statusEl.textContent = message;
      statusEl.classList.add('error');
    }
  </script>
</body>
</html>
