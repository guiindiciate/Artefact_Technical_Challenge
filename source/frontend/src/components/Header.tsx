import Image from "next/image";
import layout from "../app/page.module.css";

type Props = { title: string };

export default function Header({ title }: Props) {
  return (
    <div className={layout.topHeader}>
      <Image
        src="/artefact-logo.png"
        alt="Artefact"
        width={180}
        height={48}
        className={layout.footerImage}
        priority={false}
      />
      <h1 className={layout.header}>{title}</h1>
    </div>
  );
}
