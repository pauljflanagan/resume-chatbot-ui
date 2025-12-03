import './App.css';
import { Chat } from './pages/chat/chat';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';

function App() {
  // Use basename only in production (GitHub Pages)
  const basename = import.meta.env.PROD ? '/resume-chatbot-ui' : undefined;

  return (
    <ThemeProvider>
      <Router basename={basename}>
        <div className='w-full h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white'>
          <Routes>
            <Route path='/' element={<Chat />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
