import { createBrowserRouter, RouterProvider} from 'react-router-dom';
import Layout from '../components/Layout';
import App from '../pages/App/App';

function Router() {

  const BrowserRoutes = createBrowserRouter([{
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <App></App>,
      },
    ]
  }]);

  return (
    <RouterProvider router={BrowserRoutes} />
  );
}

export default Router;