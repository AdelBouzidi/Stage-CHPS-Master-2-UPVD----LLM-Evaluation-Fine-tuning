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
  do i = 1, numbers_len
    read(*,*) numbers(i)
  end do

  ! Initialize with first two elements
  min_idx1 = 1
  min_idx2 = 2
  min_diff = abs(numbers(min_idx1) - numbers(min_idx2))

  ! Find the closest pair
  do i = 1, numbers_len
    do j = i+1, numbers_len
      if (abs(numbers(i) - numbers(j)) < min_diff) then
        min_diff = abs(numbers(i) - numbers(j))
        min_idx1 = i
        min_idx2 = j
      end if
    end do
  end do

  ! Output the result
  if (numbers(min_idx1) < numbers(min_idx2)) then
    closest1 = numbers(min_idx1)
    closest2 = numbers(min_idx2)
  else
    closest1 = numbers(min_idx2)
    closest2 = numbers(min_idx1)
  end if

  write(*,*) closest1, closest2

  deallocate(numbers)
end program find_closest_elements