import { useAuth0 } from '@auth0/auth0-react';
import { motion } from 'framer-motion';
import Profile from './components/Profile';
import LogoutButton from './components/LogoutButton';
import Background from './components/Background';
import Landing from './components/Landing';

function App() {
  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#050714] flex items-center justify-center">
        <motion.div
          animate={{ 
            rotate: 360,
            scale: [1, 1.2, 1]
          }}
          transition={{ 
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="rounded-full h-16 w-16 border-t-2 border-b-2 border-cyan-500"
        />
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-black font-['Playfair_Display']">
      <Background />
      
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/50 to-black pointer-events-none" />
      
      <div className="relative z-10">
        {!isAuthenticated ? (
          <Landing />
        ) : (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative container mx-auto px-6 py-12"
          >
            <div className="flex justify-end mb-8">
              <LogoutButton />
            </div>
            <Profile />
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default App;