import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

interface LLMDropdownProps {
  selected: string;
  options: string[];
  setSelected: (option: string) => void;
}

export default function LLMDropdown(props: LLMDropdownProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className='relative'>
      <button
        onClick={() => setOpen(!open)}
        className='flex items-center gap-2 px-3 py-1.5 text-sm border rounded-lg bg-background hover:bg-muted transition-colors dark:border-zinc-600'
      >
        <span>{props.selected}</span>
        <ChevronDown
          size={14}
          className={`transition-transform ${open ? 'rotate-180' : ''}`}
        />
      </button>

      {open && (
        <div className='absolute bottom-full left-0 mb-2 w-48 border rounded-lg bg-background shadow-lg dark:border-zinc-600 z-10'>
          {props.options.map((opt) => (
            <div
              key={opt}
              onClick={() => {
                props.setSelected(opt);
                setOpen(false);
              }}
              className={`px-3 py-2 cursor-pointer hover:bg-muted transition-colors first:rounded-t-lg last:rounded-b-lg ${
                opt === props.selected ? 'bg-muted' : ''
              }`}
            >
              {opt}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
