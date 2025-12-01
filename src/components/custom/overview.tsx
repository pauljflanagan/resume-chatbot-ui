import { motion } from 'framer-motion';
import { MessageCircle, BotIcon } from 'lucide-react';
import ProfilePhoto from '@/assets/fonts/professional_profile_photo.jpg';

export const Overview = () => {
  return (
    <>
    <motion.div
      key="overview"
      className="max-w-3xl mx-auto md:mt-20"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ delay: 0.75 }}
    >
      <div className="rounded-xl p-6 flex flex-col gap-8 leading-relaxed text-center max-w-xl">
        <p className="flex flex-row justify-center gap-4 items-center">
          <img src={ProfilePhoto} alt="Profile" className="w-16 h-16 rounded-full object-cover" />
          <span>+</span>
          <BotIcon size={44}/>
          <span>+</span>
          <MessageCircle size={44}/>
        </p>
        <p>
          Welcome to <strong>pauLLM</strong><br />
          a resume-based chatbot based off the<br />
          professional experience of <strong>Paul Flanagan</strong>.
        </p>
      </div>
    </motion.div>
    </>
  );
};
