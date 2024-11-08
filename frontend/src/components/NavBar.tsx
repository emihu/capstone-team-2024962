import logo from "../assets/Logo.jpeg";

function NavBar() {
  return (
    <>
      <nav className="navbar bg-body-tertiary">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            <img
              src={logo}
              alt="Logo"
              width="30"
              height="30"
              className="d-inline-block align-text-top"
            />
            SkyClear
          </a>
        </div>
      </nav>
    </>
  );
}

export default NavBar;
