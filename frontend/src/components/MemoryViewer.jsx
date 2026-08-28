import React, { useEffect, useState } from "react";
import { addMemory, deleteMemory, getMemory } from "../services/api";

const MemoryViewer = () => {
  const [items, setItems] = useState([]);
  const [category, setCategory] = useState("preference");
  const [content, setContent] = useState("");

  const refresh = async () => {
    const data = await getMemory();
    setItems(data.items || []);
  };

  useEffect(() => {
    refresh();
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;
    await addMemory({ category, content });
    setContent("");
    await refresh();
  };

  return (
    <section className="card">
      <h2>Memory</h2>
      <form onSubmit={submit}>
        <input value={category} onChange={(e) => setCategory(e.target.value)} placeholder="category" />
        <input value={content} onChange={(e) => setContent(e.target.value)} placeholder="memory content" />
        <button type="submit">Add</button>
      </form>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            [{item.category}] {item.content}
            <button type="button" onClick={() => deleteMemory(item.id).then(refresh)}>Delete</button>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default MemoryViewer;
