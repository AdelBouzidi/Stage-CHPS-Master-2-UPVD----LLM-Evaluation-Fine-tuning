program find_closest_elements
  implicit none
  integer, parameter :: rk = kind(1.0d0)
  integer :: numbers_len
  real(rk), allocatable :: numbers(:)
  real(rk) :: closest1, closest2
  integer :: i, j, min_idx1, min_idx2
  real(rk) :: diff

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  do i = 1, numbers_len
    read(*,*) numbers(i)
  end do

  ! Find the two closest elements
  min_idx1 = 1
  min_idx2 = 2
  diff = abs(numbers(min_idx1) - numbers(min_idx2))

  do i = 3, numbers_len
    do j = 1, i - 1
      if (abs(numbers(i) - numbers(j)) < diff) then
        diff = abs(numbers(i) - numbers(j))
        min_idx1 = j
        min_idx2 = i
      end if
    end do
  end do

  ! Output the result
  if (numbers(min_idx1) < numbers(min_idx2)) then
    print *, numbers(min_idx1), numbers(min_idx2)
  else
    print *, numbers(min_idx2), numbers(min_idx1)
  end if

end program find_closest_elements