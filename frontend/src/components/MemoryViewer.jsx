import React, { useEffect, useState } from "react";
import { addMemory, deleteMemory, getMemory } from "../services/api";

export default function MemoryViewer() {
  const [items, setItems] = useState([]);
  const [category, setCategory] = useState("preference");
  const [content, setContent] = useState("");

  const load = () => getMemory().then(({ data }) => setItems(data));

  useEffect(() => {
    load();
  }, []);

  const onAdd = async (event) => {
    event.preventDefault();
    if (!content.trim()) return;
    await addMemory(category, content);
    setContent("");
    await load();
  };

  return (
    <section className="card">
      <h2>Memory Viewer</h2>
      <form onSubmit={onAdd}>
        <input value={category} onChange={(event) => setCategory(event.target.value)} placeholder="Category" />
        <input value={content} onChange={(event) => setContent(event.target.value)} placeholder="Memory" />
        <button type="submit">Add</button>
      </form>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.category}</strong>: {item.content}
            <button type="button" onClick={() => deleteMemory(item.id).then(load)}>Delete</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
