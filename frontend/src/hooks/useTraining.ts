import { useState, useCallback, useRef, useEffect } from 'react'
import type { Sentence, TrainingMode } from '../types'
import { trainingApi } from '../api'

/** 获取匿名用户 ID（localStorage 持久化） */
function getAnonymousId(): string {
  let id = localStorage.getItem('anonymous_id')
  if (!id) {
    id = `anon_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`
    localStorage.setItem('anonymous_id', id)
  }
  return id
}

export interface TrainingState {
  sentence: Sentence | null
  wordStates: boolean[]          // true = 标记为删除（灰字）, false = 保留（黑字）
  mode: TrainingMode
  targetTag: string | null
  timeSpent: number
  isCompleted: boolean
  isLoading: boolean
  error: string | null
}

export function useTraining() {
  const [state, setState] = useState<TrainingState>({
    sentence: null,
    wordStates: [],
    mode: 'normal',
    targetTag: null,
    timeSpent: 0,
    isCompleted: false,
    isLoading: false,
    error: null,
  })
  const startTime = useRef<number>(0)
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  // 开始计时
  const startTimer = useCallback(() => {
    startTime.current = Date.now()
    timerRef.current = setInterval(() => {
      setState(prev => ({ ...prev, timeSpent: Math.floor((Date.now() - startTime.current) / 1000) }))
    }, 1000)
  }, [])

  // 停止计时
  const stopTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
  }, [])

  // 加载句子
  const loadSentence = useCallback(async (mode: TrainingMode = 'normal', tag?: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null, isCompleted: false }))
    try {
      const sentence = await trainingApi.getSentence(mode, tag)
      const words = sentence.content.split(' ')
      setState({
        sentence,
        wordStates: new Array(words.length).fill(false),
        mode,
        targetTag: tag || null,
        timeSpent: 0,
        isCompleted: false,
        isLoading: false,
        error: null,
      })
      startTimer()
    } catch (e) {
      setState(prev => ({ ...prev, isLoading: false, error: '加载句子失败，请检查网络连接' }))
    }
  }, [startTimer])

  // 点击切换词状态
  const toggleWord = useCallback((index: number) => {
    setState(prev => {
      if (prev.isCompleted) return prev
      const newStates = [...prev.wordStates]
      newStates[index] = !newStates[index]
      return { ...prev, wordStates: newStates }
    })
  }, [])

  // 重置
  const reset = useCallback(() => {
    setState(prev => ({
      ...prev,
      wordStates: new Array(prev.wordStates.length).fill(false),
      timeSpent: 0,
      isCompleted: false,
    }))
    startTimer()
  }, [startTimer])

  // 提交
  const submit = useCallback(() => {
    stopTimer()
    setState(prev => ({ ...prev, isCompleted: true }))
    return {
      sentence_id: state.sentence!.id,
      deleted_words: state.wordStates
        .map((v, i) => (v ? i : -1))
        .filter(i => i !== -1),
      time_spent: state.timeSpent,
      training_mode: state.mode,
    }
  }, [state.sentence, state.wordStates, state.timeSpent, state.mode, stopTimer])

  // 清理计时器
  useEffect(() => {
    return () => { stopTimer() }
  }, [stopTimer])

  return {
    ...state,
    loadSentence,
    toggleWord,
    reset,
    submit,
    stopTimer,
  }
}
