import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { cx } from 'classix';
import { SparklesIcon } from './icons';
import { Markdown } from './markdown';
import { message } from '../../interfaces/interfaces';
import { MessageActions } from '@/components/custom/actions';

export const PreviewMessage = ({ message }: { message: message }) => {
  return (
    <motion.div
      className='w-full mx-auto max-w-3xl px-4 group/message'
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      data-role={message.role}
    >
      <div
        className={cx(
          'group-data-[role=user]/message:bg-zinc-700 dark:group-data-[role=user]/message:bg-muted group-data-[role=user]/message:text-white flex gap-4 group-data-[role=user]/message:px-3 w-full group-data-[role=user]/message:w-fit group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl group-data-[role=user]/message:py-2 rounded-xl'
        )}
      >
        {message.role === 'assistant' && (
          <div className='size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border'>
            <SparklesIcon size={14} />
          </div>
        )}

        <div className='flex flex-col w-full'>
          {message.content && (
            <div className='flex flex-col gap-4 text-left'>
              <Markdown>{message.content}</Markdown>
            </div>
          )}

          {message.role === 'assistant' && <MessageActions message={message} />}
        </div>
      </div>
    </motion.div>
  );
};

export const ThinkingMessage = () => {
  const role = 'assistant';
  const [dotCount, setDotCount] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setDotCount((prev) => (prev % 3) + 1);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div
      className='w-full mx-auto max-w-3xl px-4 group/message'
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1, transition: { delay: 0.2 } }}
      data-role={role}
    >
      <div className='flex gap-4 w-full'>
        <div className='size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border'>
          <SparklesIcon size={14} />
        </div>

        <div className='flex flex-col w-full'>
          <div className='relative overflow-hidden rounded-lg'>
            <div className='absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent dark:via-white/10 animate-shimmer'></div>
            <div className='px-3 py-2'>
              <span className='text-gray-400 dark:text-gray-500 text-sm'>
                Formulating a response{'.'.repeat(dotCount)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
