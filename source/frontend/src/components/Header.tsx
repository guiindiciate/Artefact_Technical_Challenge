import Image from "next/image";
import layout from "../app/page.module.css";

type Props = { title: string };

export default function Header({ title }: Props) {
  return (
    <div className={layout.headerBar}>
      <div className={layout.left}>
        <Image
          src="/artefact-logo.png"
          alt="Artefact"
          width={180}
          height={48}
          className={layout.logo}
        />
        <h1 className={layout.title}>{title}</h1>
      </div>

      <a
        href="https://www.artefact.com/company/about-us/"
        target="_blank"
        rel="noreferrer"
        className={layout.aboutBtn}
      >
        About Artefact
      </a>
    </div>
  );
}