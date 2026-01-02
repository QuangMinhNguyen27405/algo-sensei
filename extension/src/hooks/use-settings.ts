import { useEffect, useState } from "react";

type Theme = "system" | "light" | "dark";

interface AppearanceSettings {
  theme: Theme;
}

interface SystemSettings {
  notifications: boolean;
  syncInterval: number;
}

interface UISettings {
  activeTab: string;
}

const STORAGE_KEYS = {
  appearance: "appearanceSettings",
  system: "systemSettings",
  ui: "uiSettings",
};

const DEFAULT_APPEARANCE: AppearanceSettings = {
  theme: "system",
};

const DEFAULT_SYSTEM: SystemSettings = {
  notifications: true,
  syncInterval: 15,
};

const DEFAULT_UI: UISettings = {
  activeTab: "home",
};

export function useSettings() {
  const [appearance, setAppearance] =
    useState<AppearanceSettings>(DEFAULT_APPEARANCE);
  const [system, setSystem] = useState<SystemSettings>(DEFAULT_SYSTEM);
  const [ui, setUI] = useState<UISettings>(DEFAULT_UI);
  const [loading, setLoading] = useState(true);

  // Load settings from Chrome storage
  useEffect(() => {
    const loadSettings = async () => {
      try {
        const result = await chrome.storage.sync.get([
          STORAGE_KEYS.appearance,
          STORAGE_KEYS.system,
          STORAGE_KEYS.ui,
        ]);

        if (result[STORAGE_KEYS.appearance]) {
          setAppearance(result[STORAGE_KEYS.appearance] as AppearanceSettings);
        }
        if (result[STORAGE_KEYS.system]) {
          setSystem(result[STORAGE_KEYS.system] as SystemSettings);
        }
        if (result[STORAGE_KEYS.ui]) {
          setUI(result[STORAGE_KEYS.ui] as UISettings);
        }
      } catch (error) {
        console.error("Failed to load settings:", error);
      } finally {
        setLoading(false);
      }
    };

    loadSettings();
  }, []);

  const updateAppearance = async (newSettings: Partial<AppearanceSettings>) => {
    const updated = { ...appearance, ...newSettings };
    setAppearance(updated);
    try {
      await chrome.storage.sync.set({
        [STORAGE_KEYS.appearance]: updated,
      });
    } catch (error) {
      console.error("Failed to save appearance settings:", error);
    }
  };

  const updateSystem = async (newSettings: Partial<SystemSettings>) => {
    const updated = { ...system, ...newSettings };
    setSystem(updated);
    try {
      await chrome.storage.sync.set({
        [STORAGE_KEYS.system]: updated,
      });
    } catch (error) {
      console.error("Failed to save system settings:", error);
    }
  };

  const updateUI = async (newSettings: Partial<UISettings>) => {
    const updated = { ...ui, ...newSettings };
    setUI(updated);
    try {
      await chrome.storage.sync.set({
        [STORAGE_KEYS.ui]: updated,
      });
    } catch (error) {
      console.error("Failed to save UI settings:", error);
    }
  };

  const resetSettings = async () => {
    setAppearance(DEFAULT_APPEARANCE);
    setSystem(DEFAULT_SYSTEM);
    setUI(DEFAULT_UI);
    try {
      await chrome.storage.sync.clear();
    } catch (error) {
      console.error("Failed to reset settings:", error);
    }
  };

  return {
    appearance,
    system,
    ui,
    loading,
    updateAppearance,
    updateSystem,
    updateUI,
    resetSettings,
  };
}
