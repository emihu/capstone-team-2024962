import React from "react";
import { Link } from "react-router-dom";

import logo from "../assets/Logo.png";

function NavBar() {
  return (
    <>
      {/* <nav className="navbar bg-body-tertiary">
      </nav> */}
      <nav className="navbar sticky-top navbar-expand-lg navbar-light bg-light">
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
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link" to="/about">
                  About
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/how-to-use">
                  How to Use
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/">
                  Flight Predictor
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
}

export default NavBar;
