import { useAuth0 } from "@auth0/auth0-react";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <motion.button 
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => loginWithRedirect()}
      className="group px-10 py-4 bg-blue-500/10 hover:bg-blue-500/15 text-white text-sm tracking-[0.12em] uppercase font-light font-['Inter'] rounded-full transition-all duration-300 border border-blue-500/10 flex items-center gap-3"
    >
      Bring Your App On Chain
      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform opacity-60" />
    </motion.button>
  );
};

export default LoginButton; 