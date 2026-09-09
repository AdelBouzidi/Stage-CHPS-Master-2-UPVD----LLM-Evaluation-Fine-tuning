program find_closest_elements
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: closest1, closest2
  integer :: i, j, min_idx1, min_idx2
  real(dp) :: min_diff

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers

  ! Initialize minimum difference and indices
  min_diff = huge(min_diff)
  min_idx1 = 1
  min_idx2 = 2

  ! Find the two closest numbers
  do i = 1, numbers_len - 1
    do j = i + 1, numbers_len
      real(dp) :: diff
      diff = abs(numbers(i) - numbers(j))
      if (diff < min_diff) then
        min_diff = diff
        min_idx1 = i
        min_idx2 = j
      end if
    end do
  end do

  ! Output the two closest numbers in order
  if (numbers(min_idx1) < numbers(min_idx2)) then
    closest1 = numbers(min_idx1)
    closest2 = numbers(min_idx2)
  else
    closest1 = numbers(min_idx2)
    closest2 = numbers(min_idx1)
  end if

  print *, closest1, closest2

end program find_closest_elements