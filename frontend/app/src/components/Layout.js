import Navbar from "./Navbar";
import { Helmet, HelmetProvider } from "react-helmet-async";

const Layout = ({ title, content, children }) => {
  console.log(__dirname);
  return (
    <HelmetProvider>
      <Helmet>
        <title>{title}</title>
        <meta name="description" content={content} />
      </Helmet>
      <div
        className="card bg-green-700 w-screen h-screen bg-origin-border bg-center bg-no-repeat bg-cover"
        style={{ backgroundImage: "url(/images/main.jpg)" }}
      >
        <Navbar />
        {children}
      </div>
    </HelmetProvider>
  );
};

export default Layout;
