import { useAuth0 } from "@auth0/auth0-react";
import { motion } from "framer-motion";
import { Mail, User, Shield } from "lucide-react";

const Profile = () => {
  const { user, isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <div>Loading ...</div>;
  }

  return (
    isAuthenticated && (
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="backdrop-blur-lg bg-white/5 p-8 rounded-2xl border border-white/10 max-w-2xl mx-auto relative overflow-hidden"
      >
        <motion.div 
          className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 opacity-50"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3]
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        
        <motion.div 
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          className="relative flex items-center gap-6 mb-8"
        >
          <motion.img 
            whileHover={{ scale: 1.1 }}
            src={user?.picture} 
            alt={user?.name} 
            className="rounded-full w-24 h-24 border-4 border-cyan-500/50 shadow-lg shadow-cyan-500/20"
          />
          <div>
            <h2 className="text-3xl font-bold text-white">{user?.name}</h2>
            <p className="text-gray-400">{user?.email}</p>
          </div>
        </motion.div>

        <div className="relative grid grid-cols-2 gap-4">
          <motion.div 
            whileHover={{ scale: 1.02 }}
            className="bg-white/5 p-6 rounded-xl border border-white/5 flex items-start gap-4"
          >
            <User className="w-5 h-5 text-cyan-400 mt-1" />
            <div>
              <p className="text-gray-400 text-sm">User ID</p>
              <p className="text-white font-mono text-sm mt-1">{user?.sub}</p>
            </div>
          </motion.div>
          
          <motion.div 
            whileHover={{ scale: 1.02 }}
            className="bg-white/5 p-6 rounded-xl border border-white/5 flex items-start gap-4"
          >
            <Shield className="w-5 h-5 text-cyan-400 mt-1" />
            <div>
              <p className="text-gray-400 text-sm">Email Verified</p>
              <p className="text-white mt-1">{user?.email_verified ? 'Yes' : 'No'}</p>
            </div>
          </motion.div>
        </div>
      </motion.div>
    )
  );
};

export default Profile; 