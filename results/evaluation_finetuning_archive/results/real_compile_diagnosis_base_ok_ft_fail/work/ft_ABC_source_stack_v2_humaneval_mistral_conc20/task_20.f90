program find_closest_elements
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: result1, result2
  integer :: i, j, min_idx1, min_idx2
  real(dp) :: min_diff

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  do i = 1, numbers_len
    read(*,*) numbers(i)
  end do

  ! Find closest pair
  min_diff = huge(0.0_dp)
  min_idx1 = 1
  min_idx2 = 2
  do i = 1, numbers_len - 1
    do j = i + 1, numbers_len
      diff = abs(numbers(i) - numbers(j))
      if (diff < min_diff) then
        min_diff = diff
        min_idx1 = i
        min_idx2 = j
      end if
    end do
  end do

  result1 = min(numbers(min_idx1), numbers(min_idx2))
  result2 = max(numbers(min_idx1), numbers(min_idx2))

  ! Output result
  print *, result1, result2

end program find_closest_elements