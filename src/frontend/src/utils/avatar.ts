import defaultUserAvatar from '../assets/user.svg'

const DEV_USER_ASSET_PATH = '/src/assets/user.svg'

export const getUserAvatarSrc = (avatar?: string | null) => {
  const normalizedAvatar = avatar?.trim()

  if (!normalizedAvatar || normalizedAvatar === DEV_USER_ASSET_PATH) {
    return defaultUserAvatar
  }

  return normalizedAvatar
}

export const fallbackToDefaultUserAvatar = (event: Event) => {
  const target = event.target as HTMLImageElement | null

  if (target && target.src !== defaultUserAvatar) {
    target.src = defaultUserAvatar
  }
}
