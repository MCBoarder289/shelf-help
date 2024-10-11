import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HomePage } from './pages/Home.page';
import { Privacy } from './pages/Privacy.page';

const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/privacy',
    element: <Privacy />
  }
]);

export function Router() {
  return <RouterProvider router={router} />;
}