// Kept independent of the DOM so stories can be tested before connecting Supabase.
const storyImageTypes = new Set(['image/jpeg','image/png','image/webp']);
const storyVideoTypes = new Set(['video/mp4','video/webm','video/quicktime']);
const storyContactTypes = new Set(['none','phone','email']);

export function validateStoryInput({title,starting_point,progress,results,contact_type='none',contact_value='',consent=false}) {
  const t=String(title||'').trim(), start=String(starting_point||'').trim(), prog=String(progress||'').trim(), result=String(results||'').trim();
  if(t.length<8||t.length>100) return 'Title must be 8–100 characters.';
  if(start.length<20||start.length>2000) return 'Describe the starting situation in 20–2000 characters.';
  if(prog.length<20||prog.length>2000) return 'Describe what changed in 20–2000 characters.';
  if(result.length<20||result.length>2000) return 'Describe observed results in 20–2000 characters.';
  if(!consent) return 'Consent to publish your story is required.';
  if(!storyContactTypes.has(contact_type)) return 'Invalid contact type.';
  if(contact_type!=='none'&&!String(contact_value||'').trim()) return 'Enter a contact detail or choose no contact.';
  if(contact_type==='email'&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact_value)) return 'Enter a valid email.';
  if(contact_type==='phone'&&!/^\+?[0-9 ()-]{7,22}$/.test(contact_value)) return 'Enter a valid phone number.';
  return null;
}
export function validateStoryFile(file) {
  if(!file) return null;
  if(!storyImageTypes.has(file.type)&&!storyVideoTypes.has(file.type))return 'Please choose a JPEG/PNG/WebP photo or MP4/WebM/MOV video.';
  if(file.size>25*1024*1024)return 'Media must be 25 MB or smaller.';
  return null;
}
export const isSupportedStoryVideo=type=>storyVideoTypes.has(type);
