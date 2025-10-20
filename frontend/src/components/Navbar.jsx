import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-red-500 text-white p-4 flex gap-4">
      <Link to="/">Dashboard</Link>
      <Link to="/history">History</Link>
      <Link to="/status">Device Status</Link>
    </nav>
  );
}
