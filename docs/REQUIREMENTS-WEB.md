# ResumeBuilder02 - Web Requirements

## Overview

ResumeBuilder02 Web is a modern NextJS application that provides a user-friendly interface for tailoring resumes using AI. It communicates with the ResumeBuilder02 API to process resume uploads and generate tailored content.

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **Form Handling**: React Hook Form + Zod validation
- **HTTP Client**: Native fetch API with custom wrapper
- **State Management**: React Context API (for simple state) / Zustand (if needed)
- **File Upload**: react-dropzone
- **UI Components**: Custom components (based on style guide)
- **Icons**: lucide-react
- **Loading States**: Custom spinner component
- **Package Manager**: pnpm (or npm/yarn)

## Project Structure

```
web/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Home page (upload form)
│   │   ├── results/
│   │   │   └── page.tsx         # Results page
│   │   ├── globals.css          # Global styles + Tailwind
│   │   └── api/                 # API route handlers (if needed)
│   ├── components/
│   │   ├── ui/                  # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Textarea.tsx
│   │   │   ├── RadioGroup.tsx
│   │   │   ├── FileUpload.tsx
│   │   │   ├── Spinner.tsx
│   │   │   └── ErrorMessage.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   └── Container.tsx
│   │   ├── resume/
│   │   │   ├── UploadForm.tsx   # Main upload form component
│   │   │   ├── ModelSelector.tsx
│   │   │   ├── ResultsHeader.tsx
│   │   │   ├── MatchScoreCard.tsx
│   │   │   ├── TailoredResumeSection.tsx
│   │   │   ├── CoverLetterSection.tsx
│   │   │   └── ImprovementsSection.tsx
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts        # API client wrapper
│   │   │   └── endpoints.ts     # API endpoint definitions
│   │   ├── types/
│   │   │   ├── api.ts           # API response types
│   │   │   └── form.ts          # Form types
│   │   ├── utils/
│   │   │   ├── formatters.ts    # Text formatting utilities
│   │   │   └── validators.ts    # Form validators
│   │   └── constants.ts         # App constants
│   ├── hooks/
│   │   ├── useResumeUpload.ts   # Custom hook for resume upload
│   │   └── useLocalStorage.ts   # Persist form data
│   └── styles/
│       └── components/          # Component-specific styles (if needed)
├── public/
│   ├── favicon.ico
│   └── images/
├── .env.local
├── .env.example
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

## Environment Variables

```bash
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=60000  # 60 seconds

# Feature Flags (optional)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

## Pages & Routing

### Home Page (`/`)

Main entry point with resume upload form.

**Features**:
- File upload dropzone (.docx only)
- Job description textarea
- Model selection (radio buttons)
- Form validation
- Loading state with custom spinner
- Error messages display
- Responsive layout

---

### Results Page (`/results`)

Displays tailored resume, cover letter, and suggestions.

**Features**:
- Match score display (original & revised)
- Tailored resume section
- Cover letter section
- Improvement suggestions list
- "Start Over" button
- Responsive layout
- Print-friendly styling (future)

**Data Flow**:
- Results passed via URL search params (session ID) or Context API
- Fetch results from API using session ID
- Display loading state while fetching
- Handle errors gracefully

---

## Components Architecture

### UI Components (`components/ui/`)

All UI components follow the style guide (monochrome, monospace, black borders, rounded corners).

#### `Button.tsx`
```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}
```

**Variants**:
- `primary`: Black background, white text
- `secondary`: White background, black border
- `outline`: Transparent background, black border

---

#### `Card.tsx`
```tsx
interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'sm' | 'md' | 'lg';
}
```

**Styling**:
- White background
- 2px black border
- Rounded corners (lg, xl, 2xl variants)
- Responsive padding

---

#### `FileUpload.tsx`
```tsx
interface FileUploadProps {
  accept: string;
  maxSize: number;  // in bytes
  onFileSelect: (file: File) => void;
  error?: string;
  disabled?: boolean;
}
```

**Features**:
- Drag & drop support (react-dropzone)
- Click to browse
- File validation (type, size)
- Preview of selected file
- Clear file button
- Error state styling

---

#### `Spinner.tsx`
```tsx
interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  fullScreen?: boolean;  // Overlay mode
  message?: string;
}
```

**Styling**:
- Custom CSS animation (rotating border)
- Black color scheme
- Optional overlay with backdrop
- Optional loading message

---

#### `RadioGroup.tsx`
```tsx
interface RadioOption {
  value: string;
  label: string;
  description?: string;
}

interface RadioGroupProps {
  name: string;
  options: RadioOption[];
  value: string;
  onChange: (value: string) => void;
  error?: string;
}
```

---

### Resume Components (`components/resume/`)

#### `UploadForm.tsx`

Main form component for home page.

**Props**: None (self-contained)

**State**:
- File upload state
- Job description text
- Selected model
- Form errors
- Loading state

**Validation** (using Zod):
```tsx
const uploadFormSchema = z.object({
  resumeFile: z.instanceof(File)
    .refine(file => file.name.endsWith('.docx'), 'Only .docx files allowed')
    .refine(file => file.size <= 10 * 1024 * 1024, 'File must be under 10MB'),
  jobDescription: z.string()
    .min(50, 'Job description must be at least 50 characters')
    .max(10000, 'Job description too long'),
  modelId: z.enum(['gpt-4o-mini', 'mistral:instruct'])
});
```

**Submission Flow**:
1. Validate form inputs
2. Show loading spinner overlay
3. Create FormData with file + fields
4. POST to `/api/resume/tailor`
5. On success: Navigate to `/results` with data
6. On error: Display error message, hide spinner

---

#### `ModelSelector.tsx`

Radio button component for model selection.

**Props**:
```tsx
interface ModelSelectorProps {
  value: string;
  onChange: (modelId: string) => void;
  models: Array<{ id: string; name: string; description: string }>;
}
```

**Features**:
- Fetch available models from API on mount
- Display model name and description
- Highlight selected model
- Responsive layout

---

#### `MatchScoreCard.tsx`

Displays resume match percentage.

**Props**:
```tsx
interface MatchScoreCardProps {
  score: number;  // 0-100
  label: string;
  variant?: 'original' | 'revised';
}
```

**Styling**:
- Large, prominent score display
- Visual indicator (color changes based on score range)
  - 0-60: Red accent
  - 61-80: Yellow accent
  - 81-100: Green accent
- Takes up 15% of viewport (as per requirements)

---

#### `TailoredResumeSection.tsx`

Displays the tailored resume content.

**Props**:
```tsx
interface TailoredResumeSectionProps {
  resumeText: string;
  revisedScore: number;
}
```

**Features**:
- Section heading
- Revised match score display
- Resume content with preserved formatting
- Copy to clipboard button
- Download as .docx button (future)
- Print button

---

#### `CoverLetterSection.tsx`

Displays the generated cover letter.

**Props**:
```tsx
interface CoverLetterSectionProps {
  coverLetterText: string;
}
```

**Features**:
- Section heading
- Cover letter content with preserved formatting
- Copy to clipboard button
- Download as .docx button (future)

---

#### `ImprovementsSection.tsx`

Displays list of improvement suggestions.

**Props**:
```tsx
interface ImprovementsSectionProps {
  improvements: string[];
}
```

**Features**:
- Section heading
- Bulleted list of suggestions
- Highlight key action items
- Expandable items for long suggestions (future)

---

## API Integration

### API Client (`lib/api/client.ts`)

Wrapper around fetch with error handling, timeouts, and request/response interceptors.

```tsx
class APIClient {
  private baseURL: string;
  private timeout: number;

  constructor(baseURL: string, timeout: number = 60000) {
    this.baseURL = baseURL;
    this.timeout = timeout;
  }

  async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    // Implementation with AbortController for timeout
    // Error handling and response parsing
    // Type-safe responses
  }

  async uploadFile<T>(
    endpoint: string,
    formData: FormData
  ): Promise<T> {
    // Specialized method for file uploads
  }
}

export const apiClient = new APIClient(
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
);
```

---

### API Endpoints (`lib/api/endpoints.ts`)

Type-safe API endpoint definitions.

```tsx
import { apiClient } from './client';
import type {
  ModelsResponse,
  TailorResumeResponse,
  HealthResponse
} from '@/lib/types/api';

export const resumeAPI = {
  // Get available models
  getModels: async (): Promise<ModelsResponse> => {
    return apiClient.request<ModelsResponse>('/api/models');
  },

  // Tailor resume
  tailorResume: async (
    resumeFile: File,
    jobDescription: string,
    modelId: string
  ): Promise<TailorResumeResponse> => {
    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    formData.append('job_description', jobDescription);
    formData.append('model_id', modelId);

    return apiClient.uploadFile<TailorResumeResponse>(
      '/api/resume/tailor',
      formData
    );
  },

  // Health check
  healthCheck: async (): Promise<HealthResponse> => {
    return apiClient.request<HealthResponse>('/api/health');
  }
};
```

---

## Type Definitions

### API Types (`lib/types/api.ts`)

```tsx
export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  description: string;
}

export interface ModelsResponse {
  models: ModelInfo[];
}

export interface TailorResumeResponse {
  id: string;
  created_at: string;
  model_used: string;
  original_match_score: number;
  revised_match_score: number;
  tailored_resume: string;
  cover_letter: string;
  improvements: string[];
  processing_time_ms: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
}

export interface APIError {
  detail: string;
}
```

---

### Form Types (`lib/types/form.ts`)

```tsx
export interface UploadFormData {
  resumeFile: File | null;
  jobDescription: string;
  modelId: string;
}

export interface UploadFormErrors {
  resumeFile?: string;
  jobDescription?: string;
  modelId?: string;
  general?: string;
}
```

---

## Custom Hooks

### `useResumeUpload.ts`

Encapsulates resume upload logic and state management.

```tsx
interface UseResumeUploadReturn {
  uploadResume: (data: UploadFormData) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  result: TailorResumeResponse | null;
  reset: () => void;
}

export function useResumeUpload(): UseResumeUploadReturn {
  // Implementation
  // Handles API call, loading state, errors
  // Stores result in state
}
```

**Usage**:
```tsx
const { uploadResume, isLoading, error, result } = useResumeUpload();

const handleSubmit = async (data: UploadFormData) => {
  await uploadResume(data);
  if (result) {
    router.push('/results');
  }
};
```

---

## Styling

### Tailwind Configuration (`tailwind.config.ts`)

Align with style guide (monochrome, monospace).

```ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        mono: ['var(--font-mono)', 'monospace'],
      },
      colors: {
        primary: {
          black: '#000000',
          white: '#FFFFFF',
        },
        accent: {
          yellow: '#CA8A04',
          green: '#16A34A',
          red: '#DC2626',
        },
        gray: {
          50: '#F9FAFB',
          100: '#F3F4F6',
          400: '#9CA3AF',
          600: '#4B5563',
          700: '#374151',
        }
      },
      borderRadius: {
        'section': '1rem',
        'card': '0.75rem',
      },
      spacing: {
        'section': '15vh',  // For match score section
      }
    },
  },
  plugins: [],
};
export default config;
```

---

### Global Styles (`app/globals.css`)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --font-mono: ui-monospace, Menlo, Monaco, 'Cascadia Code', 'Courier New', monospace;
}

body {
  @apply font-mono bg-white text-black;
}

/* Custom Spinner Animation */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  @apply w-16 h-16 border-4 border-black border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

/* Print Styles (Future) */
@media print {
  .no-print {
    display: none;
  }
}
```

---

## Component Styling Examples

### Button Component
```tsx
const variantClasses = {
  primary: 'bg-black text-white hover:bg-gray-800',
  secondary: 'bg-white text-black border-2 border-black hover:bg-gray-50',
  outline: 'bg-transparent text-black border-2 border-black hover:bg-gray-50'
};

const sizeClasses = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-6 py-3 text-base',
  lg: 'px-8 py-4 text-lg'
};
```

### Card Component
```tsx
const baseClasses = 'bg-white border-2 border-black rounded-xl';
const paddingClasses = {
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8'
};
```

---

## Error Handling

### Error Display Strategy
1. **Form Validation Errors**: Display inline below each field
2. **API Errors**: Display in alert banner at top of form
3. **Network Errors**: Show retry button with error message
4. **File Upload Errors**: Display in file upload component

### Error Boundary
Wrap app in Next.js error boundary for unexpected errors.

```tsx
// app/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md p-8 border-2 border-black rounded-xl">
        <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
        <p className="mb-4">{error.message}</p>
        <button onClick={reset} className="btn-primary">
          Try again
        </button>
      </div>
    </div>
  );
}
```

---

## Loading States

### Page-Level Loading
Use Next.js `loading.tsx` for route transitions.

```tsx
// app/loading.tsx
export default function Loading() {
  return <Spinner fullScreen message="Loading..." />;
}
```

### Component-Level Loading
Use custom loading states within components.

```tsx
{isLoading && <Spinner message="Processing your resume..." />}
```

---

## Responsive Design

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### Responsive Patterns
- Stack form fields vertically on mobile
- Side-by-side layout for model selector on desktop
- Full-width sections on mobile, max-width container on desktop
- Hide some text/descriptions on mobile, show on desktop

---

## Accessibility

### Requirements
- ARIA labels for all interactive elements
- Keyboard navigation support
- Focus indicators on all inputs/buttons
- Screen reader friendly (semantic HTML)
- Color contrast ratios meet WCAG AA standards
- Error messages associated with form fields

### Testing
- Test with keyboard-only navigation
- Test with screen reader (VoiceOver, NVDA)
- Run Lighthouse accessibility audit

---

## Performance Optimization

### Techniques
- Code splitting with dynamic imports
- Image optimization with Next.js `<Image>` component
- Lazy load results page components
- Debounce textarea input (if real-time validation)
- Cache API responses (React Query in future)

### Bundle Size Target
- First Load JS: < 100kB gzipped
- Total Bundle: < 300kB gzipped

---

## Testing Requirements

### Unit Tests (Vitest or Jest)
- Test all utility functions
- Test form validation logic
- Test custom hooks
- Test UI component rendering

### Integration Tests (React Testing Library)
- Test form submission flow
- Test error handling scenarios
- Test API integration with mocked responses

### E2E Tests (Playwright - Future)
- Test complete user journey
- Test file upload
- Test results page display

### Coverage Target
- Minimum 80% code coverage
- All critical user paths covered

---

## SEO & Metadata

### Root Layout Metadata
```tsx
export const metadata: Metadata = {
  title: 'ResumeBuilder02 - AI-Powered Resume Tailoring',
  description: 'Tailor your resume for any job with AI assistance',
  keywords: ['resume', 'AI', 'job application', 'cover letter'],
};
```

### Dynamic Metadata
Update page titles based on content/state.

---

## Future Enhancements

1. **User Authentication**: Login/signup with session management
2. **Resume History**: Save and manage multiple resume versions
3. **PDF Export**: Export tailored resume as PDF
4. **Real-time Preview**: Live preview of formatted resume
5. **Dark Mode**: Toggle between light/dark themes
6. **Internationalization**: Multi-language support
7. **Analytics**: Track user interactions with Vercel Analytics
8. **A/B Testing**: Test different UI variations
9. **Progressive Web App**: Offline support, installable
10. **Resume Templates**: Choose from different resume formats

---

## Development Workflow

### Local Development
```bash
pnpm install
pnpm dev
# App runs on http://localhost:3000
```

### Build
```bash
pnpm build
pnpm start
```

### Linting & Formatting
```bash
pnpm lint
pnpm format
```

### Type Checking
```bash
pnpm type-check
```

---

## Deployment

### Vercel (Recommended)
- Connect GitHub repository
- Auto-deploy on push to main branch
- Environment variables configured in Vercel dashboard
- Preview deployments for PRs

### Docker (Alternative)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## Environment-Specific Configuration

### Development
- API points to `http://localhost:8000`
- Detailed error messages
- Source maps enabled

### Production
- API points to production URL
- Generic error messages
- Source maps disabled
- Analytics enabled
