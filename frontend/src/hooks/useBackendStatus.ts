"use client";
import { useEffect, useState } from "react";
import { getBackendStatus } from "@/services/api";

export function useBackendStatus() {
  const [online, setOnline] = useState(false);

  useEffect(() => {
    let mounted = true;

    async function check() {
      try {
        await getBackendStatus();
        if (mounted) {
          setOnline(true);
        }
      } catch (e) {
        if (mounted) {
          setOnline(false);
        }
      }
    }
    check();
    const interval = setInterval(check, 60 * 12 * 1000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  return online;
}
