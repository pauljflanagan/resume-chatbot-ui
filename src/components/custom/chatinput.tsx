import { Textarea } from '../ui/textarea';
import { cx } from 'classix';
import { Button } from '../ui/button';
import { ArrowUpIcon } from './icons';
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import { useState } from 'react';
import LLMDropdown from './llm-dropdown';

interface ChatInputProps {
  question: string;
  setQuestion: (question: string) => void;
  onSubmit: (text?: string, selectedModel?: string) => void;
  isLoading: boolean;
}

const suggestedActions = [
  {
    title: 'Tell me about your',
    label: 'technical skills',
    action: 'What are your main technical skills and programming languages?',
  },
  {
    title: 'Describe your experience',
    label: 'at Wellington Management',
    action: 'Can you tell me about your experience at Wellington Management?',
  },
  {
    title: 'What projects have you',
    label: 'worked on recently?',
    action: 'What kind of projects have you worked on in your current role?',
  },
  {
    title: 'Tell me about your',
    label: 'education background',
    action: 'What is your educational background?',
  },
];

export const ChatInput = ({
  question,
  setQuestion,
  onSubmit,
  isLoading,
}: ChatInputProps) => {
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [selected, setSelected] = useState('GPT-4');
  const options = ['GPT-4', 'Claude Sonnet 4.5'];


  return (
    <div className='relative w-full flex flex-col gap-4'>
      {showSuggestions && (
        <div className='hidden md:grid sm:grid-cols-2 gap-2 w-full'>
          {suggestedActions.map((suggestedAction, index) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ delay: 0.05 * index }}
              key={index}
              className='block'
            >
              <Button
                variant='ghost'              onClick={() => {
                const text = suggestedAction.action;
                onSubmit(text, selected);
                setShowSuggestions(false);
              }}
                className='text-left border rounded-xl px-4 py-3.5 text-sm flex-1 gap-1 sm:flex-col w-full h-auto justify-start items-start'
              >
                <span className='font-medium'>{suggestedAction.title}</span>
                <span className='text-muted-foreground'>
                  {suggestedAction.label}
                </span>
              </Button>
            </motion.div>
          ))}
        </div>
      )}
      <input
        type='file'
        className='fixed -top-4 -left-4 size-0.5 opacity-0 pointer-events-none'
        multiple
        tabIndex={-1}
      />

      <div className='relative'>
        <Textarea
          placeholder='Send a message...'
          className={cx(
            'min-h-[24px] max-h-[calc(75dvh)] overflow-hidden resize-none rounded-xl text-base bg-muted pr-16 pb-16'
          )}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault();

              if (isLoading) {
                toast.error(
                  'Please wait for the model to finish its response!'
                );
              } else {
                setShowSuggestions(false);
                onSubmit(question, selected);
              }
            }
          }}
          rows={3}
          autoFocus
        />

        <div className='absolute bottom-2 left-2 right-2 flex items-center justify-between pointer-events-none'>
          <div className='pointer-events-auto'>
            <LLMDropdown options={options} selected={selected} setSelected={setSelected}/>
          </div>
          <Button
            className='rounded-full p-1.5 h-fit border dark:border-zinc-600 pointer-events-auto'
            onClick={() => onSubmit(question, selected)}
            disabled={question.length === 0}
          >
            <ArrowUpIcon size={14} />
          </Button>
        </div>
      </div>
    </div>
  );
};
