import "../../App";

import React from "react";

import { Card, Col } from "react-bootstrap";
import { Link, NavLink } from "react-router-dom";
// import { Button, Alert, Breadcrumb, Card, Form, Jumbotron} from "react-bootstrap"

const VCard = ({ movie }) => {
  return (
    <React.Fragment>
      <Col
        key={`card-${movie.safe_title}`}
        md="4"
        style={{ marginBottom: "15px", marginTop: "15px" }}
      >
        <Card>
          <Card.Body>
            <Link to={`/movie/${movie.safe_title}`}>
              <img
                src={movie.cover}
                className="card-img-top"
                alt={movie.safe_title}
              />
            </Link>
            <Link to={`/movie/${movie.safe_title}`}>
              <p>{movie.title}</p>
            </Link>
            <p>
              Tomatometer
              <img
                src="https://www.rottentomatoes.com/assets/pizza-pie/images/icons/tomatometer/certified_fresh.75211285dbb.svg"
                alt="tomatometer icon"
                height="25px"
                width="25px"
              ></img>
              : {movie.score}
            </p>
            <p>
              Audience Score
              <img
                src="https://www.rottentomatoes.com/assets/pizza-pie/images/icons/audience/aud_score-fresh.6c24d79faaf.svg"
                alt="audience score icon"
                height="25px"
                width="25px"
              ></img>
              : {movie.audience_score}
            </p>
          </Card.Body>
        </Card>
      </Col>
    </React.Fragment>
  );
};

const Cast = ({ cast }) => {
  return (
    <div>
      {" "}
      <div
        style={{
          marginBottom: "2px",
          textAlign: "left",
        }}
      >
        <h3>Cast</h3>
      </div>
      {Object.keys(cast).map((i) => {
        return (
          <div
            key={`cast-${i}`}
            style={{
              marginBottom: "2px",
              textAlign: "left",
              // overflowWrap: "break-word",
              // wordBreak: "break-all",
            }}
          >
            <Link to={`/cast/${i}`}>{cast[i].name}</Link>:{" "}
            {cast[i].role !== "" ? cast[i].role : "N/A"}
          </div>
        );
      })}
    </div>
  );
};

const CastMemberCard = ({ celeb }) => {
  if (!celeb) {
    return null;
  }

  return (
    <Card style={{ marginTop: "15px" }}>
      <Card.Body>
        <Col
          key={`card-${celeb}-info`}
          md="3"
          style={{
            marginBottom: "15px",
            marginTop: "15px",
            textAlign: "center",
          }}
        >
          <Link to={`/cast/${celeb.safe_name}`}>
            <img src={celeb.image} className="card-img-top" alt="..." />
          </Link>
          <Link to={`/cast/${celeb.safe_name}`}>
            <p>{celeb.name}</p>
          </Link>
          <p>Birthday : {celeb.birthday}</p>
        </Col>
      </Card.Body>
    </Card>
  );
};

export { VCard, Cast, CastMemberCard };
