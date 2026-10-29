import { spawnSync } from 'node:child_process';
const commands = [
  ['rivalscope-backend', 'run', 'db:generate'],
  ['rivalscope-backend', 'run', 'typecheck'],
  ['rivalscope-backend', 'run', 'lint'],
  ['rivalscope-backend', 'test'],
  ['rivalscope-backend', 'run', 'test:e2e'],
  ['rivalscope-backend', 'run', 'build'],
  ['rivalscope-frontend', 'run', 'lint'],
  ['rivalscope-frontend', 'run', 'build'],
];
for (const [cwd, ...args] of commands) {
  const result = spawnSync(process.platform === 'win32' ? 'npm.cmd' : 'npm', args, { cwd, stdio: 'inherit', shell: process.platform === 'win32' });
  if (result.status !== 0) process.exit(result.status || 1);
}
