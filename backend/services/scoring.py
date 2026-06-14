"""评分计算服务
PRD §4 模块二/三：差异计算 + 速度评分
"""

def calculate_scores(core_indices: list[int], user_deleted: list[int], time_spent: int):
    """
    计算删除正确率、核心保留率、阅读压缩指数

    Args:
        core_indices: 标准压缩版本保留词索引列表
        user_deleted: 用户标记为删除的词索引列表
        time_spent: 用时（秒）

    Returns:
        dict: {core_retention, deletion_accuracy, compression_index, errors}
    """
    user_deleted_set = set(user_deleted)
    core_set = set(core_indices)

    # 正确删除的干扰词：用户删了且不在核心词中
    correctly_deleted = user_deleted_set - core_set
    # 错误删除的核心词：用户删了但在核心词中
    falsely_deleted = user_deleted_set & core_set
    # 遗漏未删的干扰词：用户没删但不在核心词中（总干扰词 = 总词数 - 核心词数）
    # 需要知道总词数，由调用方传入或从句子中计算
    # 这里在调用时计算

    # 错误详情
    errors = []
    for idx in falsely_deleted:
        errors.append({
            'type': 'false_delete',
            'index': idx,
            'explanation': '这是核心词，不应删除'
        })
    for idx in correctly_deleted:
        errors.append({
            'type': 'correct_delete',
            'index': idx,
            'explanation': '正确删除的干扰词'
        })

    return {
        'correctly_deleted': sorted(correctly_deleted),
        'falsely_deleted': sorted(falsely_deleted),
        'errors': errors
    }


def calculate_full_scores(
    core_indices: list[int],
    user_deleted: list[int],
    total_words: int,
    time_spent: int
):
    """
    完整评分计算

    PRD 模块三：阅读压缩指数 = (核心保留率 × 删除正确率) / 用时
    """
    user_deleted_set = set(user_deleted)
    core_set = set(core_indices)

    correctly_deleted = user_deleted_set - core_set
    falsely_deleted = user_deleted_set & core_set

    # 总干扰词数 = 总词数 - 核心词数
    total_noise = total_words - len(core_indices)
    # 用户应保留的核心词 = 应保留但用户确实保留的
    correctly_retained = core_set - user_deleted_set

    # 核心保留率：用户保留且正确的核心词 / 系统标准核心词数
    core_retention = (len(correctly_retained) / len(core_indices)) * 100 if core_indices else 0

    # 删除正确率：用户正确删除的干扰词 / 系统标准删除词数
    standard_deletions = [i for i in range(total_words) if i not in core_set]
    deletion_accuracy = (len(correctly_deleted) / len(standard_deletions)) * 100 if standard_deletions else 100

    # 阅读压缩指数
    compression_index = (core_retention * deletion_accuracy) / max(time_spent, 1)

    # 错误详情 for LLM
    errors = []
    for idx in falsely_deleted:
        errors.append({
            'type': 'false_delete',
            'index': idx,
            'explanation': '这是核心词，不应删除'
        })
    missed = set(range(total_words)) - core_set - user_deleted_set
    for idx in missed:
        errors.append({
            'type': 'missed_delete',
            'index': idx,
            'explanation': '这是干扰词，应删除'
        })

    return {
        'core_retention': round(core_retention, 1),
        'deletion_accuracy': round(deletion_accuracy, 1),
        'compression_index': round(compression_index, 2),
        'correctly_deleted': sorted(correctly_deleted),
        'falsely_deleted': sorted(falsely_deleted),
        'missed_deletions': sorted(missed),
        'errors': errors,
    }
