cd enclov-AI
mkdir frontend
cd frontend
npx create-next-app@latest .

npx create-next-app@latest qubuhub-enclovai
cd qubuhub-enclovai
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
cd enclov-AI

npx create-next-app@latest frontend --typescript
cd enclov-AI/frontend
npm run dev
cd enclov-AI

npm create vite@latest frontend -- --template react
cd frontend
npm install
