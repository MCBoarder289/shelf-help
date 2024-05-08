import { Welcome } from '../components/Welcome/Welcome';
import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';
import { HeaderSimple } from '@/components/HeaderSimple/HeaderSimple';
import { AppShell, Text, rem } from '@mantine/core';
import { useHeadroom } from '@mantine/hooks';

const lorem =
  'Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos ullam, ex cum repellat alias ea nemo. Ducimus ex nesciunt hic ad saepe molestiae nobis necessitatibus laboriosam officia, reprehenderit, earum fugiat?';


export function HomePage() {
  const pinned = useHeadroom({ fixedAt: 120 });
  return (
    <>
     <AppShell header={{ height: 60, offset: false }} padding="md">
      <AppShell.Header>
        <HeaderSimple />
      </AppShell.Header>

      <AppShell.Main pt={`calc(${rem(60)} + var(--mantine-spacing-md))`}>
        
        {Array(40)
          .fill(0)
          .map((_, index) => (
            <Text size="lg" key={index} my="md" maw={600} mx="auto">
              {lorem}
            </Text>
          ))}
      </AppShell.Main>
    </AppShell>
    </>
  );
}
