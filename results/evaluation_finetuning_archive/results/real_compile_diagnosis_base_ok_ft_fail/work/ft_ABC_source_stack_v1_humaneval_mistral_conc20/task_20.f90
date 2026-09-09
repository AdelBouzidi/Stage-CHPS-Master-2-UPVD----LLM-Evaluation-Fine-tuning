program main
  implicit none
  integer, parameter :: n = 6
  real :: numbers(n)
  integer :: i
  real :: min_diff, diff
  integer :: idx1, idx2
  real :: result1, result2

  ! Read input
  read(*,*) n
  do i = 1, n
    read(*,*) numbers(i)
  end do

  ! Initialize with first two elements
  idx1 = 1
  idx2 = 2
  min_diff = abs(numbers(idx1) - numbers(idx2))

  ! Find the closest pair
  do i = 1, n-1
    do j = i+1, n
      diff = abs(numbers(i) - numbers(j))
      if (diff < min_diff) then
        min_diff = diff
        idx1 = i
        idx2 = j
      end if
    end do
  end do

  ! Output the result (smaller first, larger second)
  if (numbers(idx1) < numbers(idx2)) then
    result1 = numbers(idx1)
    result2 = numbers(idx2)
  else
    result1 = numbers(idx2)
    result2 = numbers(idx1)
  end if

  print *, result1, result2
end program main