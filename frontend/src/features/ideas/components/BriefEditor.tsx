import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card } from '../../../components/ui/Card';
import { Input } from '../../../components/ui/Input';
import { Textarea } from '../../../components/ui/Textarea';
import { Button } from '../../../components/ui/Button';

const briefSchema = z.object({
  theme: z.string().min(1, 'Theme is required'),
  constraints: z.string(),
  inspirations: z.string(),
  style: z.string(),
});

type BriefFormValues = z.infer<typeof briefSchema>;

interface BriefEditorProps {
  onSubmit: (data: BriefFormValues) => void;
  isGenerating?: boolean;
}

export function BriefEditor({ onSubmit, isGenerating }: BriefEditorProps) {
  const { register, handleSubmit, formState: { errors } } = useForm<BriefFormValues>({
    resolver: zodResolver(briefSchema),
    defaultValues: {
      theme: '',
      constraints: '',
      inspirations: '',
      style: ''
    }
  });

  return (
    <Card className="p-6 border-t-4 border-t-primary-500">
      <div className="mb-6">
        <h3 className="text-xl font-semibold text-surface-900 dark:text-white">Creative Brief</h3>
        <p className="text-sm text-surface-500 dark:text-surface-400">Define parameters for AI idea generation</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="Central Theme"
          placeholder="e.g., The intersection of nature and digital life"
          error={errors.theme?.message}
          {...register('theme')}
        />
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Textarea
            label="Constraints"
            placeholder="e.g., Must use recycled materials, under 2 meters tall"
            {...register('constraints')}
          />
          <Textarea
            label="Inspirations"
            placeholder="e.g., Brutalist architecture, organic forms"
            {...register('inspirations')}
          />
        </div>
        
        <Input
          label="Preferred Style"
          placeholder="e.g., Minimalist, Abstract, Kinetic"
          {...register('style')}
        />

        <div className="pt-4 flex justify-end">
          <Button 
            type="submit" 
            variant="primary" 
            size="lg"
            isLoading={isGenerating}
            disabled={isGenerating}
          >
            {isGenerating ? 'Generating...' : 'Save Brief & Generate'}
          </Button>
        </div>
      </form>
    </Card>
  );
}
