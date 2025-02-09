import { useAuth0 } from "@auth0/auth0-react";
import { motion } from "framer-motion";
import { LogOut } from "lucide-react";

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
      className="px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-lg transition-all flex items-center gap-2"
    >
      <LogOut className="w-4 h-4" />
      Log Out
    </motion.button>
  );
};

export default LogoutButton; 